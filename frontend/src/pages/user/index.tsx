import { useAuth } from "@/contexts/auth";
import { Button } from "@/components/ui/button";

const UserPage = () => {
  const { data } = useAuth();

  const handleSignOut = () => {
    window.location.href = "/api/logout";
  };

  const profileImage = data?.images?.find((img: any) => img.height === 300)?.url || data?.images?.[0]?.url

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-6 text-center">
        <img
          src={profileImage}
          alt={data?.display_name || 'User'}
          className="h-48 w-48 rounded-full object-cover border-4 border-green-500"
        />

        <h1 className="text-3xl font-bold">
          {data?.display_name || 'User'}
        </h1>

        <p className="text-lg text-gray-600">
          User Role: <span className="font-semibold">{data?.user_role || 'User'}</span>
        </p>

        <Button
          onClick={handleSignOut}
          className="bg-green-500 hover:bg-green-600 mt-4"
        >
          Sign Out
        </Button>
      </div>
    </div>
  );
};

export default UserPage;
