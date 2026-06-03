import React, { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import toast from 'react-hot-toast';

const roles = [
  "Software Engineer",
  "Data Analyst",
  "Cloud Engineer",
  "Product Manager",
  "DevOps Engineer"
];

export default function RoleSelector() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStartInterview = async () => {
    if (!selectedRole) {
      toast.error('Please select a role');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/interviews/start`,
        {
          user_id: 1, // TODO: Get from auth
          role: selectedRole
        }
      );

      toast.success('Interview started!');
      router.push(`/interview/${response.data.id}`);
    } catch (error) {
      toast.error('Failed to start interview');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">
          AI Interview Twin
        </h1>
        <p className="text-gray-600 text-center mb-8">
          Select a role to start your interview
        </p>

        <div className="space-y-3 mb-8">
          {roles.map((role) => (
            <button
              key={role}
              onClick={() => setSelectedRole(role)}
              className={`w-full p-4 rounded-lg text-left font-semibold transition-all ${
                selectedRole === role
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {role}
            </button>
          ))}
        </div>

        <button
          onClick={handleStartInterview}
          disabled={loading}
          className={`w-full py-3 rounded-lg font-bold text-white transition-all ${
            loading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'Starting...' : 'Start Interview'}
        </button>
      </div>
    </div>
  );
}
