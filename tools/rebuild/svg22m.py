"""AS 9702/22 Feb/Mar 2026: static answer-option images (string with a cross at an antinode). python3 svg22m.py ../../assets"""
import sys, os
sys.argv=[sys.argv[0]]+sys.argv[1:]
sys.path.insert(0,'.')
import svg24
from imglib import save
OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'
if __name__=='__main__':
    # n-loop strings (Figure 5.1 is random: 2, 3 or 4 loops). Antinode i at u=(2i+1)/(2n); node at 1/n; quarter-way; near the fixed end
    import math
    for n in (2,3,4):
        i=n//2
        crosses=[((2*i+1)/(2*n),(-1)**i),(1/n,0),(0.75/n,math.sin(0.75*math.pi)),(0.05,math.sin(n*math.pi*0.05))]
        for k,c in zip('abcd',crosses): save(OUT,'as2622m_q5n%d_%s.svg'%(n,k), svg24.string(n,cross=c))
    print(sorted(f for f in os.listdir(OUT) if f.startswith('as2622m')))
