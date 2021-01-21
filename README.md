## makdi

Website crawler created for pentest exercises like HTB. 

The 2.x community versions of Burp Proxy don't include an active spider tool. This tools is designed to crawl only the internal resources found through html <  a > tags. After the links have been crawled, it will send the unique values through the proxy. The execution will end, if over a certain duration ,the internal link set has not increased or it hits the defined hard stop value.

As the links are only printed to stdout, if proxy is inaccessible, here a recording where the proxy connection has failed. 

[![asciicast](https://asciinema.org/a/CxEAxGxWLE7UlCbetQqRSOGOt.svg)](https://asciinema.org/a/CxEAxGxWLE7UlCbetQqRSOGOt?autoplay=1)
