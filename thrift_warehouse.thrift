namespace py tutorial

typedef i32 int
service Example
{
  oneway void send(1:int WAREHOUSE, 2:string action, 3:string name, 4:string productId, 5:string value),
  oneway void sendGoods(1:int WAREHOUSE, 2:string action, 3:string name, 4:string productId, 5:string value, 6: int target),
  string content(1:int target)
}