import { create } from 'zustand';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const useInterviewStore = create((set) => ({
  interview: null,
  questions: [],
  currentQuestionIndex: 0,
  evaluations: [],
  loading: false,
  error: null,

  startInterview: async (userId, role) => {
    set({ loading: true });
    try {
      const response = await axios.post(`${API_URL}/api/interviews/start`, {
        user_id: userId,
        role: role
      });
      set({ interview: response.data });
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  fetchQuestions: async (interviewId) => {
    set({ loading: true });
    try {
      const response = await axios.get(
        `${API_URL}/api/interviews/${interviewId}/questions`
      );
      set({ questions: response.data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  submitAnswer: async (interviewId, questionId, answerText) => {
    set({ loading: true });
    try {
      const response = await axios.post(
        `${API_URL}/api/evaluations/evaluate`,
        {
          interview_id: interviewId,
          question_id: questionId,
          answer_text: answerText
        }
      );
      set((state) => ({
        evaluations: [...state.evaluations, response.data],
        currentQuestionIndex: state.currentQuestionIndex + 1
      }));
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  endInterview: async (interviewId) => {
    try {
      await axios.post(`${API_URL}/api/interviews/${interviewId}/end`);
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  reset: () => {
    set({
      interview: null,
      questions: [],
      currentQuestionIndex: 0,
      evaluations: [],
      loading: false,
      error: null
    });
  }
}));
