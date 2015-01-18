# Tree structure for IAC algorithm
class node(object):
	"""docstring for node"""
	def __init__(self, cutval,dimCutVal,data,n1,n2,LE,LEM):
		super(node, self).__init__()
		self.cutval = cutval
		self.dimCutVal = dimCutVal
		self.n1 = n1
		self.n2 = n2
		self.data = data
		self.LE = LE
		self.LEM = LEM


	def display(self):
		print "cutval =",self.cutval
		print "n1 =",self.n1
		print "n2 =",self.n2
		print "data =",self.data
		pass

def status(tree,nbTab):
	for x in range(0,nbTab):
		print '    ',
		pass
	pass
'''
test = node(10,1,1,1)
test.display()
'''
