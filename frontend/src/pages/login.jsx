import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { callApi } from '../utils/axios_client';
import { useUser } from '../Usercontext';

const Login_Page = ({ onLogin }) => {
    const navigate = useNavigate();
    const [username, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const { updateUser } = useUser();

    const onFinish = async (values) => {
        try {
            const response = await callApi('/login', 'POST', {
                username: values.username,
                password: values.password,
            });

            if (response.status === 200) {
                updateUser(response.data); // 假设登录成功后返回的数据中包含用户信息
                navigate('/'); // 登录成功后跳转到首页
            } else {
                message.error('Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            message.error('Login failed');
        }
    };


    return (
        <div className="flex justify-center items-center h-screen">
            <div className="w-full max-w-md">
                <h1 className="text-3xl font-semibold mb-6 text-center">Login</h1>
                <Form
                    name="normal_login"
                    className="login-form"
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                >
                    <Form.Item
                        name="username"
                        rules={[{ required: true, message: 'Please input your Username!' }]}
                    >
                        <Input
                            prefix={<UserOutlined className="site-form-item-icon" />}
                            placeholder="Username"
                        />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        rules={[{ required: true, message: 'Please input your Password!' }]}
                    >
                        <Input
                            prefix={<LockOutlined className="site-form-item-icon" />}
                            type="password"
                            placeholder="Password"
                        />
                    </Form.Item>

                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                        //   onClick={() => handleLogin()}
                        >
                            Login
                        </Button>
                        <div className="mt-4 text-center">
                            Don't have an Account? <Link to="/register" className="text-blue-600">Sign Up</Link>
                        </div>
                    </Form.Item>
                </Form>
            </div>
        </div>
    );
};

export default Login_Page;