import Image from "next/image";
import { MyHomePage } from "@/components/my-home-page";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <MyHomePage/>
    </main>
  );
}
