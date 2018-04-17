require 'uri'
require 'net/http'
require 'http/cookie'

require 'brotli'

$jar = HTTP::CookieJar.new

def process(cookie)
    $jar.load(cookie, :format => :cookiestxt)

    http = Net::HTTP.new('refereum.com',443)
    http.use_ssl = true

    header = { "Cookie" => HTTP::Cookie.cookie_value($jar.cookies()),
               "Accept" => "*/*",
               "Accept-Encoding" => "gzip, deflate, br",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Host" => "refereum.com",
               "Upgrade-Insecure-Requests" => "1",
               "User-Agent" => "Mozilla/5.0 (X11; Linux i686; rv:58.0) Gecko/20100101 Firefox/58.0"
    }

    path = '/Prizes'

    content =''
    resp = http.get(path,header) do |str|
        content += str
    end
    decompressed =  Brotli.inflate(content)

    #puts decompressed + "\n" 

    if decompressed =~ /<h3 class="prestige\-points\-notification">([^.]+)<\/h3>/ then
         small=$1
         small.gsub!(/[\s\r\n]+/,'')
         if small =~ /<var>(\d+)<\/var>/ then
            puts $1
         end
    end


    $jar.clear()

end


#process("/home/rob/code/selenium/cookies/ref/ref_YokoNagata3.txt")

root = "/home/rob/code/selenium"
folder = root + "/cookies/ref"
index = folder + "/index2"

File.open(index, "r") do |f|
  f.each_line do |line|  
     line = line.chomp
     print "On " + line +  "\t\t\t"
     process(folder + '/' + line)
     sleep(0.15)
  end
end
