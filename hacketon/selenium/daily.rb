require 'uri'
require 'net/http'
require 'http/cookie'

#require 'brotli'

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

    path = '/Vid/Watched'

    #decompressed = Brotli.inflate(compressed)
    content =''
    resp = http.post(path,nil,header) do |str|
        content += str
    end
    #puts Brotli.inflate($content)

=begin
    sleep(0.25)
    path = '/Home/TwitterRetweetRfr'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(0.25)

    path = '/Home/TwitterRetweetOkEx'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end
=end

    $jar.clear()

end



root = "/home/rob/code/selenium"
folder = root + "/cookies/ref"
index = folder + "/index"

File.open(index, "r") do |f|
  f.each_line do |line|   
     line = line.chomp
     process(folder + '/' + line)
     sleep(0.5)
  end
end

