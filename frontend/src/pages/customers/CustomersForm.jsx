import React, { useEffect, useState } from "react";
import { Sidebar, Header } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";
import axios from "axios";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";


const CustomersForm = () => {
    const { t } = useTranslation();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const navigate = useNavigate();
    const { id } = useParams();





    return (
        <>
            <h1>Hello Perro</h1>
        </>
    )
}

export default CustomersForm;

