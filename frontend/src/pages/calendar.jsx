import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { callApi } from '../utils/axios_client';  // 引入 callApi

const CalendarComponent = () => {
    const [date, setDate] = useState(new Date());
    const [events, setEvents] = useState({});
    const calendarId = "65a94cfd79e60e18c59d8cac";  // 假设有某个日历 ID

    useEffect(() => {
        // 使用 callApi 从后端获取特定日历的事件
        callApi('GET', `/calendar/events/${calendarId}`)
            .then((response) => {
                const formattedEvents = response.data.reduce((acc, event) => {
                    const dateKey = new Date(event.startDate).toDateString();
                    acc[dateKey] = acc[dateKey] ? [...acc[dateKey], event.title] : [event.title];
                    return acc;
                }, {});
                setEvents(formattedEvents);
            })
            .catch((error) => console.error('Error fetching events:', error));
    }, [calendarId]);

    const onChange = (newDate) => {
        setDate(newDate);
        // 添加其他日期变更的处理逻辑
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
                style={{ width: '100%', height: 'auto' }}
            />
            <div className="selected-date text-lg font-semibold text-gray-700 mt-4">
                Selected date: {date.toDateString()}
            </div>
        </div>
    );
};

export default CalendarComponent;
