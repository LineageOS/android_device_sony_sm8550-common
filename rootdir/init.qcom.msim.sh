#!/vendor/bin/sh

model=$(grep -aim1 'model:' /dev/block/by-name/LTALabel | sed -e 's/^.*model:[ ]*\([A-Za-z0-9-]*\).*$/\1/I') 2> /dev/null

if [ "$model" = "" ]; then
    model=`grep -aEm1 '(A301SO|SOG10|SOG12|SO-51D|SO-53D))&nbsp;' /dev/block/by-name/LTALabel 2> /dev/null | sed -nE 's/.*((A301SO|SOG10|SOG12|SO-51D|SO-53D))&nbsp;.*/\1/p'`
fi

case "$model" in
    "XQ-BC42" | "XQ-BC52" | "XQ-BC62" | "XQ-BC72" | "XQ-BQ42" | "XQ-BQ52" | "XQ-BQ62" | "XQ-BQ72" | "XQ-DQ44" | "XQ-DQ54" | "XQ-DQ62" | "XQ-DQ72" | "XQ-DE44" | "XQ-DE54" | "XQ-DE72" )
        setprop vendor.radio.hardware.sku ds;;
    * )
        setprop vendor.radio.hardware.sku ss;;
esac

if [ "$model" = "" ]; then
    setprop vendor.radio.ltalabel.model "unknown"
else
    setprop vendor.radio.ltalabel.model "$model"
fi
