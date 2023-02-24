def getSublists(L, n):
  '''
  Write a function called getSublists, which takes as parameters a list of integers named L and an integer named n. Assume L is not empty, 0 < n <= len(L)
  This function returns a list of all possible sublists in L of length n without skipping elements in L. The sublists in the returned list should be ordered in the way they appear in L, with those sublists starting from a smaller index being at the front of the list.
  '''
  newList=[]
  for i in range(len(L)-(n-1)):
    newList.append(L[i:(n+i)])
    
  return newList
