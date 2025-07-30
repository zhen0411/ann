import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { labelsAPI } from '../../services/api';

// 异步thunk
export const fetchLabels = createAsyncThunk(
  'labels/fetchLabels',
  async (projectId, { rejectWithValue }) => {
    try {
      const response = await labelsAPI.getLabels(projectId);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '获取标签列表失败');
    }
  }
);

export const createLabel = createAsyncThunk(
  'labels/createLabel',
  async ({ projectId, data }, { rejectWithValue }) => {
    try {
      const response = await labelsAPI.createLabel(projectId, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '创建标签失败');
    }
  }
);

export const updateLabel = createAsyncThunk(
  'labels/updateLabel',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await labelsAPI.updateLabel(id, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '更新标签失败');
    }
  }
);

export const deleteLabel = createAsyncThunk(
  'labels/deleteLabel',
  async (id, { rejectWithValue }) => {
    try {
      await labelsAPI.deleteLabel(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || '删除标签失败');
    }
  }
);

const initialState = {
  labels: [],
  loading: false,
  error: null,
};

const labelsSlice = createSlice({
  name: 'labels',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    addLabel: (state, action) => {
      state.labels.push(action.payload);
    },
    updateLabelLocal: (state, action) => {
      const index = state.labels.findIndex(l => l.id === action.payload.id);
      if (index !== -1) {
        state.labels[index] = action.payload;
      }
    },
    removeLabel: (state, action) => {
      state.labels = state.labels.filter(l => l.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchLabels
      .addCase(fetchLabels.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLabels.fulfilled, (state, action) => {
        state.loading = false;
        state.labels = action.payload;
      })
      .addCase(fetchLabels.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // createLabel
      .addCase(createLabel.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createLabel.fulfilled, (state, action) => {
        state.loading = false;
        state.labels.push(action.payload);
      })
      .addCase(createLabel.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // updateLabel
      .addCase(updateLabel.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateLabel.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.labels.findIndex(l => l.id === action.payload.id);
        if (index !== -1) {
          state.labels[index] = action.payload;
        }
      })
      .addCase(updateLabel.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // deleteLabel
      .addCase(deleteLabel.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteLabel.fulfilled, (state, action) => {
        state.loading = false;
        state.labels = state.labels.filter(l => l.id !== action.payload);
      })
      .addCase(deleteLabel.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const {
  clearError,
  addLabel,
  updateLabelLocal,
  removeLabel,
} = labelsSlice.actions;

export default labelsSlice.reducer;