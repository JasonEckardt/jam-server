import { cn } from "@/lib/utils";
import Header from "@/components/Header"
import type { HTMLAttributes, Ref } from "react";
import { Outlet } from "react-router-dom";

interface MainProps extends HTMLAttributes<HTMLElement> {
  fixed?: boolean;
  ref?: Ref<HTMLElement>;
}

const AppMain = ({ fixed, className, ...props }: MainProps) => {
  return (
    <main
      className={cn(
        "peer-[.header-fixed]/header:mt-16",
        "mt-10 px-4 py-6",
        fixed && "fixed-main flex grow flex-col overflow-hidden",
        className,
      )}
      {...props}
    />
  );
};

export function Layout() {
  return (
    <>
      <Header />
      <AppMain>
        <Outlet />
      </AppMain>
    </>
  );
}

export default AppMain;
