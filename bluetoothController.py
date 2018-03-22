import bluetooth


class BlueController():
	def __init__(self, robot):
		self.robot=robot;
		self.serverSocket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		port=1
		self.serverSocket.bind(("",port))
		self.serverSocket.listen(1)
		uuid= "94f39d29-7d6d-437d-973b-fba39e49d4ee"
		bluetooth.advertise_service(self.serverSocket, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid,bluetooth.SERIAL_PORT_CLASS ],
                   profiles = [bluetooth.SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
			)
		clientSocket, address=self.serverSocket.accept()
		self.clientSocket=clientSocket
		print "Accepted connection from ", address


	def StartControlling(self):
		try:
			while True:
				data=self.clientSocket.recv(1024)
				print "Received %s" % data
				self.robot.Controlling(data)
		finally:
			print "Cleaning Up!"
			self.clientSocket.close()
			self.serverSocket.close()
