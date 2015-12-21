require 'socket'
s = UDPSocket.new

20.times do |i|
  s.send("Client message #{i+1}", 0, 'localhost', 5000)
end
