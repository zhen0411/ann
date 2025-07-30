import { configureStore } from '@reduxjs/toolkit';
import projectsReducer from './slices/projectsSlice';
import mediaReducer from './slices/mediaSlice';
import annotationsReducer from './slices/annotationsSlice';
import labelsReducer from './slices/labelsSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    projects: projectsReducer,
    media: mediaReducer,
    annotations: annotationsReducer,
    labels: labelsReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});