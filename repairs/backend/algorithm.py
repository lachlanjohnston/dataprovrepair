def project(t, attrs):
    return { t[a] for a in attrs }

def find_fds(fds, tc):
    return [ fd for fd in fds if None not in project(tc, fd.lhs) ]

def find_tuples(idx, ids, tuples, matching_fds, tc, vc):
    matches = list()
#     print(ids - vc)
    for fd in matching_fds:
#         print(ids.difference(set(vc)))
        for t_prime in ids - set(vc):
            t_prime = tuples[t_prime]
            if not fd.satisfied(t_prime, tc) and t_prime[idx] != tc[idx]:
                matches.append((fd, t_prime))
                
    return matches

def find_assignment(idx, ids, fds, tuples, t, fixed_attrs, vc):
    #     fixed_attrs = fixed_attrs.copy()
    tc = [ t[x] if x in fixed_attrs else None for x in range(len(t)) ]
#     print(list(range(len(t))))
    
    matching_fds = find_fds(fds, tc)
    t_primes = find_tuples(idx, ids, tuples, matching_fds, tc, vc)
#     print(matching_fds)
#     print(t_primes)
    
#     print('searching assign')
    while len(matching_fds) and len(t_primes):
        fd, t_prime = t_primes[0]
#         print(t_primes)
        if fd.rhs <= fixed_attrs:
            return None
        else:
            for x in fd.rhs:
                tc[x] = t_prime[x]
#             print('tc:', tc)
            matching_fds = find_fds(fds, tc)
            t_primes = find_tuples(idx, ids, tuples, matching_fds, tc, vc)
#             print('changes', t_primes)
            fixed_attrs = fixed_attrs | fd.rhs
        
    return tc