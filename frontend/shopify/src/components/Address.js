import React, {Component} from 'react';

class Address extends Component {
    handleAddAddress = () =>{
        alert()
    }
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

                <label htmlFor="add_new_address">آدرس</label>
                <input name='add_new_address' id='add_new_address'/>
                <label htmlFor="add_new_postal">کد پستی</label>
                <input type='number' name='add_new_postal' id='add_new_postal'/>
                <button onClick={this.handleAddAddress} className='btn btn-primary'>افزودن آدرس جدید</button>
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