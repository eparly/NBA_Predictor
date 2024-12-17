// src/components/Layout.tsx
import React from 'react';
import './Layout.css'; // Add shared styles here

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="layout">
      <header className="header">
        <div className="logo">EP</div>
        <nav>
          <ul className="nav-links">
            <li><a href="/">Home</a></li>
            <li><a href="/nba">NBA</a></li>
            <li><a href="/hockey">Hockey Analytics</a></li>
          </ul>
        </nav>
      </header>
      <main className="content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
