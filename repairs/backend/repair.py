import csv
import itertools
import random
import copy
from repairs.backend.fd import *
from repairs.backend.conflict_graph import *
from repairs.backend.algorithm import *

class Repair:
    def __init__(self, file):
        self.attributes, self.tuples = self.read_tsv(file)
        self.attributes_integers = range(len(self.attributes))
        self.ids = { *range(len(self.tuples)) }

        fd1 = fd(self.attributes, {'ZIP'}, {'City'})
        self.fds = [ fd1 ]
        self.idx = 0

    def run(self):
        self.cg = conflict_graph(self.idx, self.tuples, self.fds)
        self.vc = vertex_cover(self.cg)

        _, proposed_repair = self.repair(self.tuples, self.cg, self.vc)

        return self.find_alternatives(proposed_repair)

    def read_tsv(self, file_name):
        tuples = list() 
        attributes = None
        with open(file_name) as file:
            reader = csv.reader(file, delimiter="\t")
            attributes = next(reader, None)
            
            for row in reader:
                tuples.append(row)
                
        return attributes, tuples

    def repair(self, tuples, cg, vc):
        proposed = list()
        tuples_copy = copy.deepcopy(self.tuples)
    #     random.shuffle(tuples_copy)
        vc = self.vc.copy()
    #     random.shuffle(vc)
        vc = sorted(vc, key=lambda t: t[1])
        vc = list(reversed(vc))
        fd_lhs = set()
        for fd in self.fds: fd_lhs = fd_lhs | fd.rhs
    #     print(fd_lhs)
            
    #     print(vc)
        
        while len(vc):
            t, _ = vc[0]
    #         print(t)
            t = tuples_copy[t]
    #         t = tuples[int(t)].copy()
            fixed_attrs = { self.idx } # { random.choice([ x for x in attributes_integers if x not in fd_lhs ]) }
            tc = find_assignment(self.idx, self.ids, self.fds, tuples_copy, t, fixed_attrs, vc)
            
    #         print('unrepaired:', t, tc)
            while len(fixed_attrs) < len(self.attributes):
                A = random.sample(set(self.attributes_integers) - fixed_attrs, 1)[0]
                fixed_attrs.add(A)
                # find_assignment(idx, ids, fds, tuples, t, fixed_attrs, vc)
                new_tc = find_assignment(self.idx, self.ids, self.fds, tuples_copy, t, fixed_attrs, vc)
                
                if new_tc == None:
                    t[A] = tc[A]
                else:
                    tc = new_tc
    #             print(t)
            proposed.append(t)
            vc.pop(0)

        print("proposed: ", proposed)
        return tuples_copy, proposed
        
    def find_alternatives(self, proposed):
        print(len(self.cg))
        proposal_sets = list()
        added = set()
        rhs_added = set()
        l_attrs = set()
        r_attrs = set()
        for repair in proposed:
    #         print(repair)
            original = self.tuples[int(repair[self.idx])]
            
            if repair == original:
                continue
    #         print('orig', original)
            all_alternatives = list()
            options = list()
            lhses = set()
            
            for fd, t1, t2 in self.cg:
    #             print(t1, t2)
                tx = self.tuples[t1]
                ty = self.tuples[t2]
                lhs = fd.lhs
                repair_lhs = project(original, lhs)
                proposal_lhs = project(tx, lhs)
    #             print(repair_lhs)
                
                if repair_lhs == proposal_lhs:
                    lhses = (proposal_lhs) | lhses
                    r_attrs = fd.rhs | r_attrs
                    l_attrs = fd.lhs | l_attrs
                    rhs1 = None
                    rhs2 = None
                    if t1 not in added:
                        rhs1 = project(tx, fd.rhs)
                        added.add(t1)
                    if t2 not in added:
                        rhs2 = project(ty, fd.rhs)
                        added.add(t2)
                        
                    if rhs1 != None:
                        if rhs1 not in options:
                            options.append(rhs1)
                            
                            
                        all_alternatives.append(rhs1)
    #                 print(rhs2)        
                    if rhs2 != None:
                        if rhs2 not in options:
                            options.append(rhs2)
                        
                        all_alternatives.append(rhs2)
                    
    #         print('all', all_alternatives) 
    #         print(options)
            
            alternatives = list()
            for option in options:
                count = all_alternatives.count(option)
                alternatives.append((option, count))
                
            summary = lambda v, count: (list(v), count, count / len(all_alternatives))
            if len(alternatives):
                confidences = [ summary(v, count) for v, count in alternatives ]
                max_conf = max(confidences, key = lambda t: t[2])
                proposal_sets.append({ 
                    'lhs': list(lhses), 
                    'lhs_attrs': list(l_attrs),
                    'rhs_attrs': list(r_attrs),
                    'alts': confidences,
                    'max_conf': max_conf
                })
                
        return sorted(proposal_sets, key = lambda t: t['max_conf'])

    def replace(self, proposal, selection):
        print(proposal)
        for t in self.tuples:
            if project(t, proposal['lhs_attrs']) == set(proposal['lhs']):
                for attr, replacement in zip(proposal['rhs_attrs'], selection[0]):
                    t[attr] = selection[0]

        print(self.tuples)
# attributes, tuples = read_tsv('dataprovlocal/data/sample.csv')
# attributes_integers = range(len(attributes))
# tuples.append(['10', 'New York', '33109'])
# tuples.append(['9', 'Miami', '33109'])
# tuples