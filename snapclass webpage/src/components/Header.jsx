import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMenuOpen(false);
    }
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/95 backdrop-blur-sm shadow-lg' : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-purple-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <span className="ml-2 text-xl font-bold text-gray-900">SnapClass</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <button onClick={() => scrollToSection('features')} className="text-gray-700 hover:text-purple-600 transition-colors">Features</button>
            <button onClick={() => scrollToSection('audience')} className="text-gray-700 hover:text-purple-600 transition-colors">Who Uses It</button>
            <button onClick={() => scrollToSection('how-it-works')} className="text-gray-700 hover:text-purple-600 transition-colors">How It Works</button>
            <button onClick={() => scrollToSection('team')} className="text-gray-700 hover:text-purple-600 transition-colors">Team</button>
          </nav>

          <div className="hidden md:flex items-center space-x-4">
            <button className="bg-gradient-to-r from-purple-600 to-purple-500 text-white px-6 py-2 rounded-full hover:shadow-lg transform hover:scale-105 transition-all duration-200">
              Download App
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-full left-0 right-0 bg-white shadow-lg border-t">
            <nav className="flex flex-col space-y-4 p-4">
              <button onClick={() => scrollToSection('features')} className="text-gray-700 hover:text-purple-600 transition-colors text-left">Features</button>
              <button onClick={() => scrollToSection('audience')} className="text-gray-700 hover:text-purple-600 transition-colors text-left">Who Uses It</button>
              <button onClick={() => scrollToSection('how-it-works')} className="text-gray-700 hover:text-purple-600 transition-colors text-left">How It Works</button>
              <button onClick={() => scrollToSection('team')} className="text-gray-700 hover:text-purple-600 transition-colors text-left">Team</button>
              <button className="bg-gradient-to-r from-purple-600 to-purple-500 text-white px-6 py-2 rounded-full hover:shadow-lg transform hover:scale-105 transition-all duration-200 text-center">
                Download App
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;