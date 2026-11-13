"""独立来源的版本token及分页读取。"""
from .storage import canonical
from .relations import validate,predicate
import hashlib

class Source:
    def __init__(self,name,release,rows,capabilities):
        validate(rows);self.name=name;self.release=release;self.rows=rows;self.capabilities=capabilities;self.invalid=False;self.requests=[]
        self.token=hashlib.sha256(canonical([name,release,rows,capabilities])).hexdigest()
    def open(self,release):
        if self.invalid or release!=self.release:raise ValueError('来源版本不可用')
        self.requests.append({'operation':'open','release':release})
        return {'source':self.name,'release':release,'token':self.token,'capabilities':self.capabilities}
    def page(self,token,offset,limit,where=None):
        if self.invalid or token!=self.token:raise ValueError('来源句柄失效')
        if offset<0 or limit<1:raise ValueError('分页范围非法')
        rows=self.rows
        if where:
            if where['op'] not in self.capabilities['supported_ops']:raise ValueError('来源不支持下推')
            def keep(r):
                expr=dict(where);left=r[expr['column']];right=expr.get('value')
                if self.capabilities['string_order']=='casefold' and isinstance(left,str) and isinstance(right,str):left=left.casefold();right=right.casefold()
                if self.capabilities['filter_null']=='python' and expr['op']=='eq':return left==right
                return predicate({'v':left},dict(expr,column='v',value=right)) is True
            rows=[r for r in rows if keep(r)]
        output=rows[offset:offset+limit];end=offset+len(output);complete=end>=len(rows)
        self.requests.append({'operation':'page','token':token,'offset':offset,'rows':len(output)})
        return {'rows':output,'next':None if complete else end,'complete':complete}

