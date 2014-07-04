#!/bin/bash
rm coupon-*.pdf
for i in {1..2}
do
   echo "Welcome $i times"
   html2pdf coupon-$i.html coupon-$i.pdf
done
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished-coupon.pdf coupon-*.pdf

# html2pdf coupon-1.html coupon-2.html coupon-1-custom.pdf


# gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf coupon-1.pdf coupon-1-custom.pdf
