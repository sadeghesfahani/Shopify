import React, {Component} from 'react';
import './Register.css';

class Register extends Component {
    render() {
        return (
            <div className='card w-50 text-right mx-auto mt-3'>
                <div className='card-header'>
                    ثبت نام
                </div>
                <div className="card-body">
                    <form>
                        <div className='form-group'>
                            <label htmlFor="email">ایمیل</label>
                            <input type='email' className='form-control' id='email'/>
                            <label htmlFor="password">کلمه عبور</label>
                            <input type='password' className='form-control' id='password'/>
                            <label htmlFor="password1">تکرار کلمه عبور</label>
                            <input type='password' className='form-control' id='password1'/>
                            <button type="submit" className="btn btn-primary">Submit</button>
                        </div>
                    </form>

                </div>
                <div className="card-footer">
                    this is buttom
                </div>
            </div>
        );
    }
}

export default Register;