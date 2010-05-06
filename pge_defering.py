import gobject

class _DeferClass(object):
  _calls=[]
  _ref=None
  def __new__(cls,*args,**kw):
    if cls._ref is None:
      cls._ref = super(_DeferClass,cls).__new__(cls,*args,
                                                    **kw)
    return cls._ref

  def __len__(self):
    return len(self._calls)

  def __call__(self,func,*args):
    def NextCall():
      (func,args)=self._calls[0]
      func(*args)
      self._calls=self._calls[1:]
      return self._calls!=[]
    if not self._calls: gobject.idle_add(NextCall)
    self._calls.append((func,args))
