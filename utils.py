import numpy as np

def cosine_similarity(a,b):
	a = np.asarray(a)
	b = np.asarray(b)
	dot = np.dot(a, b)
	norma = np.linalg.norm(a)
	normb = np.linalg.norm(b)
	cos = dot / (norma * normb)
	return cos