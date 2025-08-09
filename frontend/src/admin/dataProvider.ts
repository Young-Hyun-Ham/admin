import type { DataProvider } from 'react-admin';

const dataProvider: DataProvider = {
  getList: async () => ({ data: [], total: 0 }),
  getOne: async () => ({ data: {} as any }),
  getMany: async () => ({ data: [] }),
  getManyReference: async () => ({ data: [], total: 0 }),
  create: async (_resource, params) => ({ data: params.data }),
  update: async (_resource, params) => ({ data: params.data }),
  updateMany: async () => ({ data: [] }),
  delete: async (_resource, params) => ({ data: params.previousData }),
  deleteMany: async () => ({ data: [] }),
};

export default dataProvider;
