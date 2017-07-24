//自定义push数据到open-falcon，go脚本
//https://book.open-falcon.org/zh/usage/data-push.html
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	// "net/url"
)

func main() {
	apiurl := "http://117.23.56.5:1988/v1/push"
	fmt.Println("URL:>", apiurl)
	type item struct {
		Endpoint    string `json:"endpoint"`
		Metric      string `json:"metric"`
		Timestamp   int64  `json:"timestamp"`
		Step        int    `json:"step"`
		Value       int64  `json:"value"`
		CounterType string `json:"counterType"`
		Tags        string `json:"tags"`
	}

	type message struct {
		Item []item `json:"item"`
	}

	//json序列化
	var post message
	post.Item = append(post.Item, item{Endpoint: "test-endpoint", Metric: "test-metric", Timestamp: 1500804940,
		Step: 60, Value: 10, CounterType: "GAUGE", Tags: "idc=xixian"})
	fmt.Println(apiurl, "post", post)

	jsonStr, _ := json.Marshal(post.Item)
	fmt.Println("jsonStr", jsonStr)
	fmt.Println("new_str", bytes.NewBuffer([]byte(jsonStr)))

	req, err := http.NewRequest("POST", apiurl, bytes.NewBuffer([]byte(jsonStr)))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))
}

结果：
/*
  URL:> http://117.23.56.5:1988/v1/push
	http://117.23.56.5:1988/v1/push post {[{test-endpoint test-metric 1500804940 60 10 GAUGE idc=xixian}]}
	jsonStr [91 123 34 101 110 100 112 111 105 110 116 34 58 34 116 101 115 116 45 101 110 100 112 111 105 110 116 34 44 34 109 101 116 114 105 99 34 58 34 116 101 115 116 45 109 101 116 114 105 99 34 44 34 116 105 109 101 115 116 97 109 112 34 58 49 53 48 48 56 48 52 57 52 48 44 34 115 116 101 112 34 58 54 48 44 34 118 97 108 117 101 34 58 49 48 44 34 99 111 117 110 116 101 114 84 121 112 101 34 58 34 71 65 85 71 69 34 44 34 116 97 103 115 34 58 34 105 100 99 61 120 105 120 105 97 110 34 125 93]
	new_str [{"endpoint":"test-endpoint","metric":"test-metric","timestamp":1500804940,"step":60,"value":10,"counterType":"GAUGE","tags":"idc=xixian"}]
	response Status: 200 OK
	response Headers: map[Date:[Mon, 24 Jul 2017 07:57:05 GMT] Content-Length:[7] Content-Type:[text/plain; charset=utf-8]]
	response Body: success
*/
