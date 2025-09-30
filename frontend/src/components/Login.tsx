import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";

const Login = () => {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-sm">
        <CardHeader className="text-center">
          <CardTitle>Jam Server</CardTitle>
          <CardDescription className="mt-2 flex flex-col gap-2">
            <p>A self-hosted Jam server to play music with your friends!</p>
            <p>
              Share a queue with your friends and connect your Spotify account to import songs into the shared queue.
            </p>
          </CardDescription>
          <CardContent className="mt-5 w-full">
            <Button asChild className="w-full bg-green-500">
              <a href="/api/login">Login with Spotify</a>
            </Button>
          </CardContent>
        </CardHeader>
      </Card>
    </div>
  );
};
export default Login;
