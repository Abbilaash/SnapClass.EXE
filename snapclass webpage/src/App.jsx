import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Vision from './components/Vision';
import Features from './components/Features';
import Audience from './components/Audience';
import HowItWorks from './components/HowItWorks';
import Team from './components/Team';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <Vision />
      <Features />
      <Audience />
      <HowItWorks />
      <Team />
      <Footer />
    </div>
  );
}

export default App;