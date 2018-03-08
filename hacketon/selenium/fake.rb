require 'uri'
require 'net/http'

#http = Net::HTTP.new('video-weaver.fra02.hls.ttvnw.net',443)
http = Net::HTTP.new('refereum.com',443)

http.use_ssl = true


#path = '/v1/playlist/CswCwvxkaePGCWFHRFU_jOA_r3Ckdx0NavNQOJYiBgp-cMJosYpPnrM6_bLK6TWfEl97HIaxqiwWB4hWuwoWkAD5fR7N-HDqtQatfa9198uF23bMlArn4FMZshsGGKmJ6zpBOPtg_3Iaf1LyeLPutI404nbTJiez8mYs9VAGKFGH8YMv-IreoZ1nACfkXqOERiUIRwAwgLhQXRaF8DPf_H9aM46Y_6sZsptVVR2k66J4OtOJjYhUrsScuWDOIfzhsyixm4Z8fGT-aUO3AHPIo-hN64MFrkTCExG0aTu65NR--mU28-gge_S-G411BaWTp-qxHyHs8Buw-RHDLZnInABFtM7zPqPOX2ZtGjwjl5Mjq2dsj_j3oI5CBZIbILvybYN_utBl6L7mZqzuD77Tod02HyMMRvkAhphwcLEZkBH4zivZRXpyC80ZI55Ds4wSEAAYg8BC6c0q7QPUjw4v3ZIaDI-rFQ5ZlAT0dKSPOw.m3u8'


path = '/Games'

# GET request -> so the host can set his cookies
resp, data = http.get(path, nil)

#cookie = resp.response['set-cookie'].split('; ')[0]

resp.each do |key, value|
   puts ">> #{key}"
   puts value
end


#puts "data: #{data}\n"

#puts "cookie : #{cookie}\n"
