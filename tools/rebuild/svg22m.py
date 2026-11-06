"""AS 9702/22 Feb/Mar 2026: static answer-option images (string with a cross at an antinode). python3 svg22m.py ../../assets"""
import sys, os
sys.argv=[sys.argv[0]]+sys.argv[1:]
sys.path.insert(0,'.')
import svg24
from imglib import save
OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'
if __name__=='__main__':
    # 3-loop string (Figure 5.1): antinodes at u=1/6, 1/2, 5/6; nodes at 0, 1/3, 2/3, 1
    crosses=[(0.5,-1),(1/3,0),(0.25,0.7071),(0.05,0.454)]
    for k,c in zip('abcd',crosses): save(OUT,'as2622m_q5bi_%s.svg'%k, svg24.string(3,cross=c))
    print(sorted(f for f in os.listdir(OUT) if f.startswith('as2622m')))
