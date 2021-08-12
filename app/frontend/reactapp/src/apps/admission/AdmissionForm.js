import React from 'react';

import { Button } from '@blueprintjs/core/lib/esm/components/button/buttons';
import { Intent } from '@blueprintjs/core/lib/esm/common/intent';

import DateInput from '../../components/dateinput';

const Level = {
    INTER: window.SERVER_DATA.constants.Level.INTER,
    BS: window.SERVER_DATA.constants.Level.BS
};

const InterAdmissionType = {
    Regular: window.SERVER_DATA.constants.InterAdmissionType.Regular,
    PFY: window.SERVER_DATA.constants.InterAdmissionType.PFY,
};

const Gender = {
    Male: window.SERVER_DATA.constants.Gender.Male,
    Female: window.SERVER_DATA.constants.Gender.Female,
};

const AdmissionSession = {
    Morning: window.SERVER_DATA.constants.AdmissionSession.Morning,
    Evening: window.SERVER_DATA.constants.AdmissionSession.Evening,
};


function cleanInteger(num) {
    let cleaned = parseInt(num);
    if (!cleaned) {
        return 0;
    }
    return cleaned;
}

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}


function redirectUrl(path, params, method = 'post') {


    const form = document.createElement('form');
    form.method = method;
    form.action = path;

    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


// function post_redirect(url, payload_name=null, payload=null) {
//     var form = document.createElement('form');
//     form.method = 'post';
//     form.action = url;

//     document.body.appendChild(form);

//     if (payload_name === null) {
//         form.submit();
//         return;
//     }
 
//     var input = document.createElement('input');
//     input.type = 'hidden';
//     input.name = payload_name;
//     input.value = payload;
//     form.appendChild(input);


//     form.submit();
// }

class AdmissionForm extends React.Component {

    constructor(props) {
        super(props);
        this.disciplines = window.SERVER_DATA.disciplines;

        this.state = {
            name: "",
            gender: Gender.Male,
            cnic: "",
            father_name: "",
            father_cnic: "",
            phone: "",
            date_of_birth: void 0,

            other_discount: 0,

            level: Level.INTER,
            semOrYear: 0, // semester or year
            admission_type: InterAdmissionType.Regular,
            adm_session: AdmissionSession.Morning,
            selectedDisciplineId: -1,
            marks: 0,

            feeDetails_full_fee: 0,
            feeDetails_marks_amount: 0,
            feeDetails_marks_slab_name: '',
            feeDetails_dicretionary_discount: 0,
            feeDetails_dicretionary_reason: '',
            feeDetails_pfy_amount: 0,
            feeDetails_num_installments: 3,
            feeDetails_adm_amount: 0,
        }
    }
 
    componentDidMount() {
        this.handleLevelChange(Level.INTER);
    }

    getSelectedDiscipline = (id=null) => {
        let targetId = id == null ? this.state.selectedDisciplineId : id;
        for (let i = 0; i < this.disciplines.length; i++) {
            if (this.disciplines[i].id ==  targetId) {
                return this.disciplines[i];
            }
        }
        return null
    }

    handleLevelChange = (level) => {
        let first_id;

        for (let i = 0; i < this.disciplines.length; i++) {
            if (this.disciplines[i].level == level) {
                first_id = this.disciplines[i].id;
                break;
            }
        }

        this.setState({
            level: level,
            semOrYear: 1
        }, () => {
            this.handleDisciplineChange(first_id);
        });
    }

    handleDisciplineChange = (discId) => {
        this.setState({
            selectedDisciplineId: discId,
            feeDetails_full_fee: this.getSelectedDiscipline(discId).fee_structure.full_fee
        }, () => {
            this.handleMarksChange(this.state.marks);
        });
    }

    handleMarksChange = (marks) => {
        let calc_marks = parseInt(marks);
        if (!calc_marks) {
            // this.setState({
                // marks: marks,
            // });
            // return;
            calc_marks = 0;
        }

        let fee_structure = this.getSelectedDiscipline().fee_structure;
        let marksAmount = fee_structure.full_fee;
        let marksSlabName = '';
        

        for (let i = 0; i < fee_structure.slabs.length; i++) {
            let slab = fee_structure.slabs[i];
            if (calc_marks >= slab.marks) {
                marksAmount = slab.amount;
                marksSlabName = slab.name;
                break;
            }
        }

        this.setState({
            marks: marks,
            feeDetails_marks_amount: marksAmount,
            feeDetails_marks_slab_name: marksSlabName,
        });
    }

    getMarksBasedDiscount() {
        return this.state.feeDetails_full_fee - this.state.feeDetails_marks_amount;
    }

    getTotalDiscount = () => {
        return this.state.feeDetails_full_fee 
                - this.state.feeDetails_marks_amount 
                + cleanInteger(this.state.feeDetails_dicretionary_discount);
    }

    getTotalPackage() {
        return this.state.feeDetails_full_fee - this.getTotalDiscount();
    }

    getTotalAmountReceived() {
        let am = cleanInteger(this.state.feeDetails_adm_amount);
        if (this.isPFYAmountEnabled()) {
            am += cleanInteger(this.state.feeDetails_pfy_amount);
        }
        return am;
    }

    getPerInstallmentAmount() {
        let num_installments = cleanInteger(this.state.feeDetails_num_installments);
        if (num_installments == 0) num_installments = 3;
        return this.getTotalPackage() / num_installments;
    }

    isPFYAmountEnabled() {
        return this.state.level == Level.INTER &&
               this.state.admission_type == InterAdmissionType.Regular &&
               this.state.semOrYear == 1;
    }

    renderPersonalInfoForm() {
        return (
            <React.Fragment>
                <h6 className="bp3-heading mb-md">Personal Information</h6>
                <div className="row row-sm">
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Student Name
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.name}
                                    onChange={(e) => this.setState({name: e.target.value})}
                                    placeholder="Enter Name"
                                />
                            </div>
                        </label>
                    </div>
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Gender
                            <div className="bp3-select bp3-fill">
                                <select 
                                    value={this.state.gender}
                                    onChange={(e) => this.setState({gender: e.target.value})}>
                                    <option value={Gender.Male}>Male</option>
                                    <option value={Gender.Female}>Female</option>
                                </select>
                            </div>
                        </label>
                    </div>
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Student CNIC
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.cnic}
                                    onChange={(e) => this.setState({cnic: e.target.value})}
                                    placeholder="Enter CNIC"
                                />
                            </div>
                        </label>
                    </div>
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Father Name
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.father_name}
                                    onChange={(e) => this.setState({father_name: e.target.value})}
                                    placeholder="Enter Name"
                                />
                            </div>
                        </label>
                    </div>
                </div>


                <div className="row row-sm">
                    <div className="col-md-4">
                        <label className="bp3-label">
                            Father CNIC
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.father_cnic}
                                    onChange={(e) => this.setState({father_cnic: e.target.value})}
                                    placeholder="Enter CNIC"
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-sm-4">
                        <label className="bp3-label">
                            Date Of Birth
                            <DateInput
                                value={this.state.date_of_birth}
                                onChange={new_date => {
                                    this.setState({ date_of_birth: new_date });
                                }}
                                serverName="date_of_birth"
                            />
                        </label>
                    </div>
                    <div className="col-sm-4">
                        <label className="bp3-label">
                            Phone/Mobile No
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.phone}
                                    onChange={(e) => this.setState({phone: e.target.value})}
                                    placeholder="Enter Phone"
                                />
                            </div>
                        </label>
                    </div>
                </div>
            </React.Fragment>
        );
    }

    renderAdmissionDetailsForm() {
        return (
            <React.Fragment>
                <h6 className="bp3-heading mt-md mb-md">Admission Details</h6>


                <div className="row row-sm">
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Level
                            <div className="bp3-select bp3-fill">
                                <select 
                                    value={this.state.level}
                                    onChange={(e) => this.handleLevelChange(e.target.value)}>
                                    <option value={Level.INTER}>Intermidiate</option>
                                    <option value={Level.BS}>B.S</option>
                                </select>
                            </div>
                        </label>
                    </div>

                    <div className="col-md-3">
                        <label className="bp3-label">
                            Discipline/Course
                            <div className="bp3-select bp3-fill">
                                <select 
                                    value={this.state.selectedDisciplineId}
                                    onChange={(e) => this.handleDisciplineChange(e.target.value)}>
                                    {this.disciplines.map((d, index) => {
                                        if (d.level == this.state.level) {
                                            return (
                                            <option
                                                // selected={d.id == this.state.selectedDisciplineId}
                                                key={d.id} 
                                                value={d.id}>

                                                    {d.name}
                                            </option>);
                                        }
                                        return null;
                                    })}
                                </select>
                            </div>
                        </label>
                    </div>

                    <div className="col-md-3">
                        <label className="bp3-label">
                            Session
                            <div className="bp3-select bp3-fill">
                                <select 
                                    value={this.state.adm_session}
                                    onChange={(e) => this.setState({adm_session: e.target.value})}>

                                    <option value={AdmissionSession.Morning}>Morning</option>
                                    <option value={AdmissionSession.Evening}>Evening</option>
                                </select>
                            </div>
                        </label>
                    </div>

                    <div className="col-md-3">
                        <label className="bp3-label">
                            Type
                            <div className="bp3-select bp3-fill">
                                <select
                                    value={this.state.admission_type}
                                    onChange={(e) => this.setState({admission_type: e.target.value})}
                                    disabled={this.state.level != Level.INTER}>

                                    <option value={InterAdmissionType.Regular}>Regular</option>
                                    <option value={InterAdmissionType.PFY}>PFY</option>

                                </select>
                            </div>
                        </label>
                    </div>
                    
                </div>

                <div className="row row-sm">
                    <div className="col-md-3">
                        {this.renderYearSelectOrSemesterInput()}
                    </div>
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Marks
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    onChange={(e) => this.handleMarksChange(e.target.value)}
                                    className="bp3-input no-intent" 
                                    value={this.state.marks} 
                                    placeholder="Enter" />
                            </div>
                        </label>
                    </div>
                </div>
            </React.Fragment>
        );
    }

    renderYearSelectOrSemesterInput() {
        if (this.state.level == Level.INTER) {
            return (
                <label className="bp3-label">
                    Year
                    <div className="bp3-select bp3-fill">
                        <select
                            value={this.state.semOrYear}
                            onChange={(e) => this.setState({semOrYear: e.target.value})}>
                            <option value={1}>1st Year</option>
                            <option value={2}>2nd Year</option>
                        </select>
                    </div>
                </label>
            );
        } else {
            return (
                <label className="bp3-label">
                    Semester
                    <div className="bp3-select bp3-fill">
                        <select
                            value={this.state.semOrYear}
                            onChange={(e) => this.setState({semOrYear: e.target.value})}>
                            <option value={1}>1st</option>
                            <option value={2}>2st</option>
                            <option value={3}>3st</option>
                            <option value={4}>4st</option>
                            <option value={5}>5st</option>
                            <option value={6}>6st</option>
                            <option value={7}>7st</option>
                            <option value={8}>8st</option>
                        </select>
                    </div>
                </label>
            );
        }
    }

    renderFeeStructureForm() {
        return (
            <React.Fragment>
                <h6 className="bp3-heading mt-md mb-md">
                    Fee Structure
                </h6>


                <div className="row row-sm">
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Full Fee
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(this.state.feeDetails_full_fee)}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>
                    
                    <div className="col-md-3">
                        <label className="bp3-label">
                            Marks Based Discount
                            <div className="bp3-input-group">
                                <div className="bp3-input-group bp3-fill">
                                    <input 
                                        className="bp3-input no-intent" 
                                        value={numberWithCommas(this.getMarksBasedDiscount())}
                                        readOnly={true}
                                    />
                                </div>
                                <div className="bp3-input-action">
                                    <span className="bp3-tag bp3-minimal bp3-intent-primary">
                                        {this.state.feeDetails_marks_slab_name == '' ? 
                                            'None': this.state.feeDetails_marks_slab_name}
                                    </span>
                                </div>
                            </div>
                        </label>
                    </div>

                    <div className="col-md-3">
                        <label className="bp3-label">
                            Other Discount
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    className="bp3-input no-intent" 
                                    value={this.state.other_discount}
                                    onChange={(e) => this.setState({other_discount: e.target.value})}
                                    placeholder="Enter Amount"
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-3">
                        <label className="bp3-label">
                            Discretionary Discount
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    className="bp3-input no-intent" 
                                    value={this.state.feeDetails_dicretionary_discount}
                                    onChange={(e) => {
                                        this.setState({feeDetails_dicretionary_discount: e.target.value})
                                    }}
                                />
                            </div>
                        </label>
                    </div>
                </div>

                <div className="row row-sm">
                    <div className="col-md-6">
                        <label className="bp3-label">
                            Reason for Discretionary Discount
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="text" 
                                    className="bp3-input no-intent" 
                                    value={this.state.feeDetails_dicretionary_reason}
                                    onChange={(e) => this.setState({feeDetails_dicretionary_reason: e.target.value})}
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-6">
                        <label className="bp3-label">
                            <strong>Total Discount</strong>
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(this.getTotalDiscount())}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>
                </div>


                <div className="row row-sm">
                    <div className="col-md-2">
                        <label className="bp3-label">
                            PFY Amount Adjusted
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    className="bp3-input no-intent" 
                                    value={this.state.feeDetails_pfy_amount}
                                    disabled={!this.isPFYAmountEnabled()}
                                    onChange={(e) => {
                                        this.setState({feeDetails_pfy_amount: e.target.value})
                                    }}
                                />
                            </div>
                        </label>
                    </div>

            
                    <div className="col-md-4">
                        <label className="bp3-label">
                            <strong>Final Package</strong>
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(this.getTotalPackage())}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-2">
                        <label className="bp3-label">
                            # Of Installments
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    className="bp3-input no-intent" 
                                    value={this.state.feeDetails_num_installments}
                                    onChange={(e) => {
                                        this.setState({feeDetails_num_installments: e.target.value})
                                    }}
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-4">
                        <label className="bp3-label">
                            Per Installment Amount
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(Math.round(this.getPerInstallmentAmount()))}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>
                </div>

                <div className="row row-sm">
                    <div className="col-md-4">
                        <label className="bp3-label">
                            Amount Received At Admission Time
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    type="number" 
                                    className="bp3-input no-intent" 
                                    value={this.state.feeDetails_adm_amount}
                                    onChange={(e) => {
                                        this.setState({feeDetails_adm_amount: e.target.value})
                                    }}
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-4">
                        <label className="bp3-label">
                            <strong>Total Amount Received</strong>
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(this.getTotalAmountReceived())}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>

                    <div className="col-md-4">
                        <label className="bp3-label">
                            <strong>Balance Amount</strong>
                            <div className="bp3-input-group bp3-fill">
                                <input 
                                    className="bp3-input no-intent" 
                                    value={numberWithCommas(this.getTotalPackage() - this.getTotalAmountReceived())}
                                    readOnly={true}
                                />
                            </div>
                        </label>
                    </div>
                </div>

            </React.Fragment>
        );
    }

    render() {
        return (
            <div>
                {this.renderPersonalInfoForm()}
                <hr />
                {this.renderAdmissionDetailsForm()}
                <hr />
                {this.renderFeeStructureForm()}

                <br />

                <Button
                    type="submit"
                    text="Submit"
                    icon="build"
                    fill={false}
                    intent={Intent.SUCCESS}
                    minimal={true}
                    outlined={true}
                    onClick={() => {
                        redirectUrl(window.SERVER_DATA.urls.new_admission, {
                            csrfmiddlewaretoken: window.CSRF_TOKEN,
                            payload_json: JSON.stringify(this.makePayload())
                        }, 'post')
                    }}
                />

            </div>
        );
    }

    makePayload() {
        return {
            college_id: window.SERVER_DATA.college.id,

            name: this.state.name,
            gender: cleanInteger(this.state.gender),
            cnic: this.state.cnic,
            father_name: this.state.father_name,
            father_cnic: this.state.father_cnic,

            phone: this.state.phone,

            // school: this.state.school,
            // address: this.state.address,

            date_of_birth: this.state.date_of_birth == void 0 ? "" : this.state.date_of_birth,
            level: cleanInteger(this.state.level),
            discipline_id: cleanInteger(this.state.selectedDisciplineId),
            adm_session: cleanInteger(this.state.adm_session), // This
            adm_type: cleanInteger(this.state.admission_type),
            semOrYear: cleanInteger(this.state.semOrYear),
            marks: cleanInteger(this.state.marks),
            full_fee: this.state.feeDetails_full_fee,
            marks_based_disc: this.getMarksBasedDiscount(),
            other_discount: 45745, // This
            discretion_disc: cleanInteger(this.state.feeDetails_dicretionary_discount),
            discretion_disc_reason: this.state.feeDetails_dicretionary_reason,
            total_disc: this.getTotalDiscount(),
            pfy_amount: cleanInteger(this.state.feeDetails_pfy_amount),
            final_package: this.getTotalPackage(),
            num_installments: cleanInteger(this.state.feeDetails_num_installments),
            adm_amount: cleanInteger(this.state.feeDetails_adm_amount),
        }
    }
};


export default AdmissionForm;
