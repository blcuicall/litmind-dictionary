port=10118
pid=$(lsof -i :$port | awk '{print $7}' | awk -F"/" '{ print $1 }');

if [  -n  "$pid"  ];  then
    kill  -9  $pid;
fi