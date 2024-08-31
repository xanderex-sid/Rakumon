"use client"; // Add this directive to mark the file as a Client Component

import React, { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import "@/app/globals.css"; // Import the CSS file with animations

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, placeholder, ...props }, ref) => {
    const placeholderTexts = [
      "Help me buy my first Laptop",
      "Jordan Ke naye shoes dikhado",
      "Show me Animated Deadpool T-shirt",
      "Sale ka Best Phone dikhado"
    ];

    const [currentPlaceholder, setCurrentPlaceholder] = useState<string>(placeholderTexts[0]);

    // Handle the cycling of placeholder texts
    useEffect(() => {
      const updatePlaceholder = () => {
        setCurrentPlaceholder((prev) => {
          const currentIndex = placeholderTexts.indexOf(prev);
          // Ensure to not show the same text twice
          const nextIndex = (currentIndex + 1) % placeholderTexts.length;
          return placeholderTexts[nextIndex];
        });
      };

      const interval = setInterval(updatePlaceholder, 5000); // Change text every 5 seconds

      return () => clearInterval(interval); // Cleanup on component unmount
    }, []);

    // Update currentPlaceholder if placeholder prop changes
    useEffect(() => {
      if (placeholder && !placeholderTexts.includes(placeholder)) {
        setCurrentPlaceholder(placeholder);
      }
    }, [placeholder]);

    return (
      <div className="relative">
        <input
          type={type}
          className={cn(
            "flex h-10 w-full min-w-[400px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-bold",
            className
          )}
          ref={ref}
          placeholder="" // Remove the placeholder here
          {...props}
        />
        <div className="absolute inset-0 flex items-center px-3 text-sm text-muted-foreground">
          <span className="animated-placeholder">{currentPlaceholder}</span>
        </div>
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
