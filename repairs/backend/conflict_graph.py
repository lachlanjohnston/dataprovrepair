import itertools

def conflict_graph(idx, tuples, fds):
    cg = list()
    for fd in fds:
        for t1, t2 in itertools.combinations(tuples, 2):
#             print(t1, t2)
            if not fd.satisfied(t1, t2):# and ( fd, t1, t2 ) not in cg:# or (fd, t2, t1) not in cg:
                cg.append(( fd, int(t1[idx]), int(t2[idx]) ))
                
    return cg

def prune(cg, tx, ty):
    cg_ = list()
    
    for fd, t1, t2 in cg:
        edge = {t1, t2}
        print(t1, t2)
        print('edge', edge)
        if tx in edge or ty in edge:
            continue
        else:
            cg_.append((fd, t1, t2))
    return cg_

def vertex_cover(cg):
    cg_ = cg
    vertices = list()
    
    while cg_:
        v = cg_[0][1:]
        
        
        count_v1 = 0
        count_v2 = 0
        
        for _, v1, v2 in cg:
            if v1 == v[0] or v1 == v[1]:
                count_v1 += 1
            if v2 == v[0] or v2 == v[1]:
                count_v2 += 1
        
               
        cg_ = prune(cg_, *v)
        v = (v[0], count_v1), (v[1], count_v2)
        vertices += v 
        print(v)
        
    return vertices

def delta_conflict_graph(idx, fds, delta):
    cg = list()
    for fd in fds:
        for t1, t2 in itertools.product(tuples, delta):
#             print(t1, t2)
            if not fd.satisfied(t1, t2):# and ( fd, t1, t2 ) not in cg:# or (fd, t2, t1) not in cg:
                cg.append(( fd, int(t1[idx]), int(t2[idx]) ))
                
    return cg