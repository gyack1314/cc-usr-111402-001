"""独立来源资料的当前读取入口。"""
from .sources import Source

def inspect(data,storage,root):
    result={}
    for name,d in data['sources'].items():
        s=Source(name,d['release'],d['rows'],d['capabilities']);h=s.open(d['release']);page=s.page(h['token'],0,1)
        result[name]={'handle':h,'first_page':page,'requests':s.requests}
    return result
