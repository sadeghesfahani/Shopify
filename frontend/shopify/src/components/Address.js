import React, {Component} from 'react';

class Address extends Component {
    generateAddress = () => {
        return (
            <>
                <label htmlFor="send_good">آدرس ارسال محصول</label>
                <select name="send_good" id='send_good'>
                    {this.props.address.length > 0 && this.props.address.map((address, index) => {
                        return <option key={index} name={address.id} value={address.id}>{address.address}</option>
                    })}
                </select>
                <label htmlFor="send_invoice">آدرس ارسال فاکتور</label>
                <select name="send_invoice" id='send_good'>
                    {this.props.address.length > 0 && this.props.address.map((address, index) => {
                        return <option key={index} name={address.id} value={address.id}>{address.address}</option>
                    })}
                </select>
            </>
        )
    }

    render() {
        return (
            <div>
                {this.generateAddress()}
            </div>
        );
    }
}

export default Address;