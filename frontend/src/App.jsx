import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/login';
import Register from './pages/register';
import CalendarComponent from './pages/calendar';
import AddEventComponent from './pages/addEvent';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/cal" element={<CalendarComponent />} />
                <Route path="/add" element={<AddEventComponent />} />
            </Routes>
        </Router>
    );
};

export default App;