require 'uri'
require 'net/http'
require 'http/cookie'

cookies = 'cookies.txt'
oauth = 'OAuth p8owv403gk4pvu7kaykfcy0ess1pio'
client = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

proxy_addr = :ENV
proxy_port = nil

if (ARGV[0])
    cookies = ARGV[0]
end

if (ARGV[1])
    oauth = ARGV[1]
end

if (ARGV[2])
    client = ARGV[2]
end

if (ARGV[3])
    proxy_addr = ARGV[3]
end

if (ARGV[4])
    proxy_port = ARGV[4]
end


#proxy_addr = '47.206.51.67'
#proxy_port = 8080

http = Net::HTTP.new('video-weaver.fra02.hls.ttvnw.net',443,proxy_addr,proxy_port)
http2 = Net::HTTP.new('gql.twitch.tv',443,proxy_addr,proxy_port)
http3 = Net::HTTP.new('api.twitch.tv',443,proxy_addr,proxy_port)

http.use_ssl = true
http2.use_ssl = true
http3.use_ssl = true

jar = HTTP::CookieJar.new

# Load from a file
jar.load(cookies, :format => :cookiestxt )

# Set the Cookie header value, where uri is the destination URI

#puts HTTP::Cookie.cookie_value(jar.cookies()) 

header2 = { "Cookie" => HTTP::Cookie.cookie_value(jar.cookies()),
           "Accept" => "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Encoding" => "gzip, deflate, br",
"Accept-Language" => "en-US,en;q=0.5",
"Connection" => "keep-alive",
"Host" => "gql.twitch.tv",
"Upgrade-Insecure-Requests" => "1",
"User-Agent" => "Mozilla/5.0 (X11; Linux i686; rv:58.0) Gecko/20100101 Firefox/58.0",
"authorization" => oauth,
"client-id" => client 
}

header3 = { "Cookie" => HTTP::Cookie.cookie_value(jar.cookies()),
	               "Accept" => "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		       "Accept-Encoding" => "gzip, deflate, br",
		       "Accept-Language" => "en-US,en;q=0.5",
		       "Connection" => "keep-alive",
		       "Host" => "api.twitch.tv",
		       "Upgrade-Insecure-Requests" => "1",
		       "User-Agent" => "Mozilla/5.0 (X11; Linux i686; rv:58.0) Gecko/20100101 Firefox/58.0",
		       "authorization" => oauth,
		       "client-id" => client
}


path = '/v1/playlist/CssCKUmAIGSZO7DAWUrUTic2V8PpYQd2yZiBX_UwHyUv8Px8wShC06hpG5T3NEZlR0yTnLmVQllrS_YtlhGoPbVi_xRUyZ-kqnyBX2tq4SdArg8d05MNwm3p40J5btYI0sURUsCigzcCyhbEHmqx9OJRXGNHPOz770kqi7PGYOA69tTJToMBNi2ASbuknr_REW_ukggmmsUesJuIspgeX0BP-lmvFVOmg6t80IjOtAQlDOM_iU-50ggmhjffxgXxa5o69zVJ2hKDucpUDrfMdvw7HNstfiK1MGi7UFtrKQQqlM-5BQxrEctEOl7WeXNO9pMhc7rkVh1MHqDfqhvcFjwaPkAW9mbUUTt-d-Kt3Jf3H0N_8wDO9XeZnXoTJLfWqGIG1e-Kju-3kGjjlo90YZp_eJNHZr0Udu6V1uVvC9_XPE8uQWgACN2dKrGUoBIQ_bqbCrnubsDklxJinvPaABoMkiyGWEJuBcdxfnWl.m3u8'

path2 = '/gql'

path3 = '/kraken/streams/eljdmax1223'

# GET request -> so the host can set his cookies
resp = http.get(path, nil)

json2 = '[ { "extensions" : { }, "operationName" : "ChannelPage_SetSessionStatus", "query" : "mutation ChannelPage_SetSessionStatus($input: SetSessionStatusInput!) { setSessionStatus(input: $input) { setAgainInSeconds __typename } }",
"variables" : { "input" : { "activity" :  { "gameID":"" , "type" :"WATCHING", "userID" : "186734999"}, "availability":"ONLINE", "sessionID": "d90ae3fda3bccb97" } }  }  ] '

resp = http2.post(path2, json2, header2)

#resp = http3.get(path3, header3)


##resp.each do |key, value|
##   puts ">> #{key}"
##   puts value
##end

##puts "data: "+resp.body + "\n"
