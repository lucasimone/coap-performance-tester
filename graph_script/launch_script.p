# Gnuplot script file for plotting data in file "courbe1.dat"
# average sucess ratio en fonction de nbre actors et sous diffrents nbre concurrent failures
# This file is called   force.p

set terminal postscript eps noenhanced defaultplex \
   leveldefault color colortext \
   dashed dashlength 3.0 linewidth 1.0 butt \
  palfuncparam 2000,0.003 \
   "Helvetica" 16
set output "e2d.eps"
set key top right noreverse enhanced autotitles box linetype -1 linewidth 1.000


set xlabel " PDR"
set ylabel "E2E Delay (s) "
set xr[0.2:1]
set ytics 0.5
set yr [0:2]
set grid 


plot  "e2e.dat" using 1:2 title "Number_reTx=4" with lp lt 5 lc rgb "red" pt 12 ps 1 lw 1, \
	"e2e.dat" using 1:3 title "Number_reTx=5 " with lp lt 2 lc rgb "blue" pt 5 ps 1 lw 1, \
	"e2e.dat" using 1:4 title "Number_reTx=6 " with lp lt 3 lc rgb "black" pt 8 ps 1 lw 1

#	f(x) title "Our technique fit" with l lw 2.5 lt 17

