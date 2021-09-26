### Command
```
while true; do (echo "--- $(date)" && top -b -n 1 | head -n 5) >> ps.log; sleep 5; done
```
