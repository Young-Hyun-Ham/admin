import { type DataProvider, fetchUtils } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

// fetchUtils.fetchJson의 options 파라미터 타입을 사용합니다. (ra-core에서 Options로 임포트 가능)
const httpClient = (url: string, options: fetchUtils.Options = {}) => {
    if (!options.headers) {
        // Headers 타입으로 명시적으로 생성
        options.headers = new Headers({ Accept: 'application/json' });
    }
    const token = localStorage.getItem('token');
    const type = localStorage.getItem('type') || 'Bearer';
    
    // set 메소드는 Headers 객체에 존재합니다.
    (options.headers as Headers).set('Authorization', `${type} ${token}`);
    
    return fetchUtils.fetchJson(url, options);
};

// DataProvider 타입을 명시적으로 지정
const dataProvider: DataProvider = simpleRestProvider(
    'http://localhost:8000/v1/api', 
    httpClient
);

export default dataProvider;