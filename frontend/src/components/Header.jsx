import React from 'react';
import { Bot } from 'lucide-react'; 

function Header() {
  return (
    <header className="py-6 border-b border-gray-700">
      <div className="container mx-auto flex items-center justify-center space-x-3">
        <Bot className="w-8 h-8 text-green-400" />
        <h1 className="text-3xl font-bold tracking-tight text-gray-100">
          Quantitative Analysis Platform
        </h1>
      </div>
    </header>
  );
}

export default Header;