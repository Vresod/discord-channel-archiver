from enum import IntEnum

class RequestType(IntEnum): # make an enum of request types; this probably already exists in requests but i couldn't find it
	GET = 1
	POST = 2
	# we dont need the rest of the types but we'll have them anyways
	PATCH = 3
	DELETE = 4
	HEAD = 5
	OPTIONS = 6
	PUT = 7
	TRACE = 8