import React, {useState} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/login';
import Register from './pages/register';
import CalendarComponent from './pages/calendar';
import AddEventComponent from './pages/addEvent';
import { UserProvider } from './Usercontext';

function App() {
    const [isLoggedIn, setLoggedIn] = useState(false);
    const [role, setRole] = useState('');
    const [username, setUsername] = useState("");
    const [userId, setUserId] = useState("");

    const handleLogin = (user) => {
        setUsername(user.username);
        setRole(user.role);
        setLoggedIn(true);
        setUserId(user.userId);
    };

    const handleLogout = () => {
        setUsername("");
        setRole("");
        setLoggedIn(false);
        setUserId("");
    };

    return (
        <Router>
            <UserProvider>
                <div>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/cal" element={<CalendarComponent />} />
                        <Route path="/add" element={<AddEventComponent />} />
                    </Routes>
                </div>

            </UserProvider>
        </Router>
    );
}
export default App;