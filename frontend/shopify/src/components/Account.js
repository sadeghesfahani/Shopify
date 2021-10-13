import React, {Component} from 'react';

class Account extends Component {
    getOrderHistory=(howmuch=false)=>{
        if (howmuch){
            const url = ""
        }
    }
    render() {
        return (
            <div>
                <nav>
                    <div className="nav nav-tabs" id="nav-tab" role="tablist">
                        <a className="nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab"
                           aria-controls="nav-home" aria-selected="true">اطلاعات کاربری</a>
                        <a className="nav-link" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab"
                           aria-controls="nav-profile" aria-selected="false">آدرس</a>
                        <a className="nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-contact" role="tab"
                           aria-controls="nav-contact" aria-selected="false">پیشینه سفارشات</a>
                    </div>
                </nav>
                <div className="tab-content" id="nav-tabContent">
                    <div className="tab-pane fade show active" id="nav-home" role="tabpanel"
                         aria-labelledby="nav-home-tab">...
                    </div>
                    <div className="tab-pane fade" id="nav-profile" role="tabpanel"
                         aria-labelledby="nav-profile-tab">...
                    </div>
                    <div className="tab-pane fade" id="nav-contact" role="tabpanel"
                         aria-labelledby="nav-contact-tab">...
                    </div>
                </div>

            </div>
        );
    }
}

export default Account;