package main

import (
	"errors"
	"flag"
	"fmt"
	"github.com/aeden/traceroute"
	"github.com/oschwald/geoip2-golang"
	"net"
	"os"
)

var (
	db geoip2.Reader
)

type Coord struct {
	TTL                 int
	Latitude, Longitude float64
	City                string
}

func printHop(db *geoip2.Reader, hop traceroute.TracerouteHop) (Coord, error) {
	addr := address(hop.Address)
	hostOrAddr := addr
	if hop.Host != "" {
		hostOrAddr = hop.Host
	}
	if hop.Success {
		loc, err := ip2loc(db, addr)
		if err == nil {
			fmt.Printf("%-3d %v (%v) %s %v\n", hop.TTL, hostOrAddr, addr, meaningfulOutput(loc), hop.ElapsedTime)
		} else {
			fmt.Printf("%-3d %v (%v)   %v\n", hop.TTL, hostOrAddr, addr, hop.ElapsedTime)
		}
		//fmt.Printf("%s %s", loc.Location.Latitude, loc.Location.Longitude)
		return Coord{hop.TTL, loc.Location.Latitude, loc.Location.Longitude, loc.City.Names["en"]}, nil
	} else {
		fmt.Printf("%-3d *\n", hop.TTL)
		return Coord{}, errors.New("get location failed")
	}
}

func ip2loc(db *geoip2.Reader, addr string) (*geoip2.City, error) {
	ip := net.ParseIP(addr)
	return db.City(ip)
}
func meaningfulOutput(loc *geoip2.City) string {
	output := ""
	for _, i := range []string{loc.Country.Names["zh-CN"], loc.City.Names["zh-CN"]} {
		output += i
	}
	return output
}

func imageURL(coords []Coord) string {
	tpl := "http://restapi.amap.com/v3/staticmap?zoom=1&size=1024*500&markers=%s&paths=%s&key=ee95e52bf08006f63fd29bcfbcf21df0"
	markers := ""
	paths := "10,,,,:"
	for n, i := range coords {
		markers += fmt.Sprintf("mid,,%d:%.4f,%.4f|", n, i.Longitude, i.Latitude)
		paths += fmt.Sprintf("%.4f,%.4f;", i.Longitude, i.Latitude)
	}
	if markers[len(markers)-1] == '|' {
		markers = markers[:len(markers)-1]
	}
	if paths[len(paths)-1] == ';' {
		paths = paths[:len(paths)-1]
	}
	return fmt.Sprintf(tpl, markers, paths)
}

func address(address [4]byte) string {
	return fmt.Sprintf("%v.%v.%v.%v", address[0], address[1], address[2], address[3])
}

func main() {
	var m = flag.Int("m", traceroute.DEFAULT_MAX_HOPS, `Set the max time-to-live (max number of hops) used in outgoing probe packets (default is 64)`)
	var q = flag.Int("q", 1, `Set the number of probes per "ttl" to nqueries (default is one probe).`)
	var d = flag.String("d", "GeoLite2-City.mmdb", `IP locate database path (default is 17monipdb.dat)`)

	flag.Parse()
	host := flag.Arg(0)
	db, err := geoip2.Open(*d)
	if err != nil {
		fmt.Printf("Unvalied IP locate database (%s) with error: %s\n", d, err.Error())
		fmt.Println("Please provider a vailided IP locate database (download from here: http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz)")
		os.Exit(1)
	}
	defer db.Close()

	options := traceroute.TracerouteOptions{}

	options.SetRetries(*q - 1)
	options.SetMaxHops(*m + 1)

	ipAddr, err := net.ResolveIPAddr("ip", host)
	if err != nil {
		return
	}

	fmt.Printf("traceroute to %v (%v), %v hops max, %v byte packets\n", host, ipAddr, options.MaxHops(), options.PacketSize())

	c := make(chan traceroute.TracerouteHop, 0)
	coords := make([]Coord, 0)
	lastCity := ""
	go func() {
		for {
			hop, ok := <-c
			if !ok {
				fmt.Println()
				return
			}
			coord, err := printHop(db, hop)
			if err == nil && coord.City != lastCity {
				lastCity = coord.City
				coords = append(coords, coord)
			}
		}
	}()

	_, err = traceroute.Traceroute(host, &options, c)
	if err != nil {
		if err.Error() == "operation not permitted" {
			fmt.Println("Operation not permitted (Maybe with sudo?)")
		} else {
			fmt.Printf("Error: ", err)
		}
	} else {
		fmt.Printf("Visualize URL: %s\n", imageURL(coords))
	}
}

/*
usage:
go run iproute.go bing.com
traceroute to bing.com (204.79.197.200), 65 hops max, 52 byte packets
1   pandorabox_2077.lan. (192.168.1.1)  1.060203ms
2   114.252.96.1 (114.252.96.1) 中国北京 5.348994ms
3   61.148.185.69 (61.148.185.69) 中国北京 5.736864ms
4   124.65.61.133 (124.65.61.133) 中国北京 7.589925ms
5   124.65.194.89 (124.65.194.89) 中国北京 7.585424ms
6   219.158.14.190 (219.158.14.190) 中国 39.953344ms
7   219.158.11.2 (219.158.11.2) 中国 55.692004ms
8   219.158.97.26 (219.158.97.26) 中国 43.479576ms
9   219.158.101.166 (219.158.101.166) 中国 44.82868ms
10  219.158.39.170 (219.158.39.170) 中国 65.228965ms
11  ae3-0.hkb-96cbe-1b.ntwk.msn.net. (191.234.84.248) 美国 50.22985ms
12  tor1.hkb.msedge.net. (131.253.5.135) 美国 53.988716ms
13  tor2.hk2.msedge.net. (131.253.5.215) 美国 51.512017ms
14  *
15  *
16  *
17  *
18  *
19  *
20  *
21  pandorabox_2077.lan. (192.168.1.1)  85.035908ms
22  *
23  pandorabox_2077.lan. (192.168.1.1)  446.773458ms
24  pandorabox_2077.lan. (192.168.1.1)  1.025469ms
25  pandorabox_2077.lan. (192.168.1.1)  897.787µs
26  114.252.96.1 (114.252.96.1) 中国北京 10.600771ms
27  114.252.96.1 (114.252.96.1) 中国北京 5.452876ms
28  114.252.96.1 (114.252.96.1) 中国北京 3.552917ms
29  61.148.185.69 (61.148.185.69) 中国北京 5.600726ms
30  61.148.185.69 (61.148.185.69) 中国北京 7.763549ms
31  61.148.185.69 (61.148.185.69) 中国北京 7.878667ms
32  124.65.61.133 (124.65.61.133) 中国北京 5.722551ms
33  124.65.61.133 (124.65.61.133) 中国北京 7.394798ms
34  124.65.61.133 (124.65.61.133) 中国北京 8.070106ms
35  124.65.194.89 (124.65.194.89) 中国北京 4.0813ms
36  124.65.194.89 (124.65.194.89) 中国北京 7.759828ms
37  124.65.194.89 (124.65.194.89) 中国北京 7.96742ms
38  219.158.14.190 (219.158.14.190) 中国 38.680327ms
39  219.158.14.190 (219.158.14.190) 中国 40.054525ms
40  219.158.14.190 (219.158.14.190) 中国 39.840022ms
41  219.158.11.14 (219.158.11.14) 中国 43.743329ms
42  219.158.11.10 (219.158.11.10) 中国 56.944486ms
43  219.158.96.226 (219.158.96.226) 中国 44.829592ms
44  219.158.96.246 (219.158.96.246) 中国 46.168254ms
45  219.158.19.89 (219.158.19.89) 中国 42.63811ms
46  219.158.96.246 (219.158.96.246) 中国 55.531853ms
47  *
48  *
49  219.158.101.166 (219.158.101.166) 中国 46.89507ms
50  219.158.101.178 (219.158.101.178) 中国 51.52412ms
51  219.158.39.170 (219.158.39.170) 中国 54.29724ms
52  219.158.39.170 (219.158.39.170) 中国 48.488625ms
53  219.158.39.170 (219.158.39.170) 中国 51.10568ms
54  ae27-0.hk2-96cbe-1b.ntwk.msn.net. (104.44.224.0) 美国雷德蒙德 47.009276ms
55  ae3-0.hkb-96cbe-1b.ntwk.msn.net. (191.234.84.248) 美国 60.14481ms
56  ae3-0.hkb-96cbe-1b.ntwk.msn.net. (191.234.84.248) 美国 49.907844ms
57  ae0-0.hk2-96cbe-1a.ntwk.msn.net. (207.46.42.64) 美国雷德蒙德 47.079828ms
58  tor5.hk2.msedge.net. (131.253.5.223) 美国 46.651123ms
59  ae0-0.hk2-96cbe-1a.ntwk.msn.net. (207.46.42.64) 美国雷德蒙德 53.496697ms
60  *
61  *
62  *
63  *
64  *
65  tor1.hkb.msedge.net. (131.253.5.135) 美国 39.135116ms

Visualize URL: http://restapi.amap.com/v3/staticmap?zoom=1&size=1024*500&markers=mid,,0:116.3883,39.9289|mid,,1:105.0000,35.0000|mid,,2:116.3883,39.9289|mid,,3:105.0000,35.0000|mid,,4:-122.1215,47.6740|mid,,5:-97.0000,38.0000|mid,,6:-122.1215,47.6740|mid,,7:-97.0000,38.0000|mid,,8:-122.1215,47.6740|mid,,9:-97.0000,38.0000&paths=10,,,,:116.3883,39.9289;105.0000,35.0000;116.3883,39.9289;105.0000,35.0000;-122.1215,47.6740;-97.0000,38.0000;-122.1215,47.6740;-97.0000,38.0000;-122.1215,47.6740;-97.0000,38.0000&key=ee95e52bf08006f63fd29bcfbcf21df0
*/
