import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

const Player = () => {
  return (
    <Card className="max-w-xl">
      <CardHeader>
        <CardTitle>Now playing...</CardTitle>
      </CardHeader>
      <CardContent></CardContent>
    </Card>
  );
};
export default Player;
