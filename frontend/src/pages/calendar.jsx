import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const CalendarComponent = () => {
    const [date, setDate] = useState(new Date());
    const [events, setEvents] = useState({});

    useEffect(() => {
        // 模擬從後端獲取事件
        // 請替換成您的 API 調用
        fetch('http://localhost:8080/calendar/get')
            .then((response) => response.json())
            .then((data) => {
                const formattedEvents = data.reduce((acc, event) => {
                    const dateKey = new Date(event.startDate).toDateString();
                    acc[dateKey] = acc[dateKey] ? [...acc[dateKey], event.title] : [event.title];
                    return acc;
                }, {});
                setEvents(formattedEvents);
            })
            .catch((error) => console.error('Error fetching events:', error));
    }, []);

    const onChange = (newDate) => {
        setDate(newDate);
        // 添加其他日期變更的處理邏輯
    };

    const tileContent = ({ date, view }) => {
        const dateKey = date.toDateString();
        if (view === 'month' && events[dateKey]) {
            return (
                <div className="events-container">
                    {events[dateKey].map((event, index) => (
                        <div key={index} className="event-indicator">{event}</div>
                    ))}
                </div>
            );
        }
    };

    return (
        <div className="calendar-component flex flex-col items-center justify-center p-4 bg-gray-100">
            <Calendar
                onChange={onChange}
                value={date}
                tileContent={tileContent}
                tileClassName="tile-day border border-gray-300 rounded p-1 text-black hover:bg-blue-100"
                className="border-0 text-lg w-full"
                // Tailwind CSS 樣式
                style={{ width: '100%', height: 'auto' }}
            />
            <div className="selected-date text-lg font-semibold text-gray-700 mt-4">
                Selected date: {date.toDateString()}
            </div>
        </div>
    );
};

export default CalendarComponent;
