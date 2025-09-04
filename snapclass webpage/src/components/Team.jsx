import React from 'react';
import { Award, Github, Linkedin } from 'lucide-react';
import abbilaashImg from '../team/abbilaash.jpg';
import nivashiniImg from '../team/nivashini.jpg';

const Team = () => {
  const teamMembers = [
    {
      name: 'A T Abbilaash',
      role: 'Hardware and ML Research',
      bio: 'Machine learning enthusiast who loves making AI accessible to everyone',
      avatar: abbilaashImg,
      github: 'https://github.com/Abbilaash',      // <--- your link here
      linkedin: 'https://www.linkedin.com/in/a-t-abbilaash-117b07270/' // <--- your link here
    },
    {
      name: 'Nivashini N',
      role: 'Frontend and AI Research',
      bio: 'AI researcher passionate about building inclusive and impactful technology',
      avatar: nivashiniImg,
      github: 'https://github.com/Nivashini2505',      // <--- your link here
      linkedin: 'https://www.linkedin.com/in/nivashini-n-493824214/' // <--- your link here
    }
  ];

  return (
    <section id="team" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            Meet Our Team
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            A passionate creators, engineers, and designers working together to democratize AI-powered learning
          </p>
          
          {/* Hackathon Badge */}
          <div className="inline-flex items-center bg-gradient-to-r from-purple-600 to-purple-500 text-white px-6 py-3 rounded-full shadow-lg">
            <Award className="mr-2" size={20} />
            <span className="font-semibold">Built during the Qualcomm Edge AI Hackathon</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 justify-center">
          {teamMembers.map((member, index) => (
            <div 
              key={index}
              className={`bg-gradient-to-br from-purple-50 to-white rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300 text-center border border-purple-100 ${index === 0 ? 'lg:col-start-2' : 'lg:col-start-3'}`}
            >
              <div className="relative mb-6">
                <img 
                  src={member.avatar} 
                  alt={member.name}
                  className="w-24 h-24 rounded-full mx-auto object-cover shadow-lg"
                />
                <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm">✨</span>
                </div>
              </div>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {member.name}
              </h3>
              
              <div className="text-purple-600 font-medium mb-3">
                {member.role}
              </div>
              
              <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                {member.bio}
              </p>
              
              <div className="flex justify-center space-x-3">
                <a
                  href={member.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-8 h-8 bg-gray-100 hover:bg-purple-100 rounded-full flex items-center justify-center transition-colors duration-200"
                >
                  <Github size={16} className="text-gray-600 hover:text-purple-600" />
                </a>
                <a
                  href={member.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-8 h-8 bg-gray-100 hover:bg-purple-100 rounded-full flex items-center justify-center transition-colors duration-200"
                >
                  <Linkedin size={16} className="text-gray-600 hover:text-purple-600" />
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Team Values */}
        <div className="mt-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-3xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-6">Our Mission</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl mb-3">🌍</div>
              <h4 className="font-semibold mb-2">Global Impact</h4>
              <p className="text-purple-100 text-sm">
                Making quality education accessible to students worldwide, regardless of their location or internet connectivity.
              </p>
            </div>
            <div>
              <div className="text-4xl mb-3">🔒</div>
              <h4 className="font-semibold mb-2">Privacy First</h4>
              <p className="text-purple-100 text-sm">
                All AI processing happens on-device, ensuring student data remains private and secure at all times.
              </p>
            </div>
            <div>
              <div className="text-4xl mb-3">🚀</div>
              <h4 className="font-semibold mb-2">Innovation</h4>
              <p className="text-purple-100 text-sm">
                Pushing the boundaries of edge AI to create powerful educational tools that work anywhere, anytime.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Team;