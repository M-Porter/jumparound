export JUMPAROUND_SOURCED=1

JUMPAROUND_FUNC="${JUMPAROUND_FUNC:-j}"

source /dev/stdin <<EOF
$JUMPAROUND_FUNC() {
    cd "\$(jumparound to)" || return
}
EOF
